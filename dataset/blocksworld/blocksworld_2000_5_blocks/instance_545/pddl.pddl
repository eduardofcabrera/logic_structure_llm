

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(on c a)
(on d b)
(on e d)
(clear c)
)
(:goal
(and
(on a b)
(on d e)
(on e a))
)
)


