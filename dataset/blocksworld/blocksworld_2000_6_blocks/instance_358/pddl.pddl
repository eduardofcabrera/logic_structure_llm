

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(on c d)
(on d b)
(ontable e)
(clear a)
(clear c)
)
(:goal
(and
(on c e)
(on d a))
)
)


