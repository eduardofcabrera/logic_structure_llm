

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c a)
(on d e)
(on e c)
(clear b)
(clear d)
)
(:goal
(and
(on a e)
(on c d)
(on d b)
(on e c))
)
)


