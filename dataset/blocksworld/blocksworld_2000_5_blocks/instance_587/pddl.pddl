

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(on c a)
(on d b)
(ontable e)
(clear c)
(clear d)
)
(:goal
(and
(on a b)
(on c d)
(on d a)
(on e c))
)
)


