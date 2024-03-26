

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b a)
(on c e)
(ontable d)
(ontable e)
(clear b)
(clear c)
)
(:goal
(and
(on a d)
(on b a)
(on c e)
(on d c))
)
)


