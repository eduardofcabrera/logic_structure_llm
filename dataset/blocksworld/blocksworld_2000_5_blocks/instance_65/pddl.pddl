

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b d)
(on c e)
(ontable d)
(ontable e)
(clear a)
(clear c)
)
(:goal
(and
(on b c)
(on c e)
(on d a))
)
)


